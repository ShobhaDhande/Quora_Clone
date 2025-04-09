from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views import View
from .models import QuestionModel,AnswerModel,LikeModel
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import localtime,now
from django.db import transaction
from django.shortcuts import get_object_or_404

class DashboardView(LoginRequiredMixin, View):
    """
    Handles GET requests to display the dashboard with a list of questions and their associated answers.

    The view:
    - Fetches all questions and their answers
    - Checks if the current user has liked or disliked any of them
    - Annotates each item with local time and like/dislike status
    - Renders the data into the dashboard.html template
    """

    def get(self, request):
        try:
            # Get the currently logged-in user
            user = request.user

            # Get the current date (for display)
            current_date = now().date()

            # Fetch all questions with selected fields, including username of the user who posted
            questions = QuestionModel.objects.values(
                'question_id', 'question', 'created_at',
                'like_count', 'dislike_count', 'user__username'
            )

            # Fetch all answers with selected fields, including username of the user who posted
            answers = AnswerModel.objects.values(
                'question_id', 'answer_id', 'answer', 'created_at',
                'like_count', 'dislike_count', 'user__username'
            )

            # Get all votes by the current user
            user_likes = LikeModel.objects.filter(user=user)

            # Initialize sets to track what user has liked/disliked
            liked_map = set()
            disliked_map = set()

            # Populate liked and disliked maps with model name and object_id
            for like in user_likes:
                key = (like.content_type.model, like.object_id)
                if like.vote_type == 'Like':
                    liked_map.add(key)
                elif like.vote_type == 'Dislike':
                    disliked_map.add(key)

            questions_list = []

            # Iterate through each question and attach answer list and like/dislike flags
            for question in questions:
                # Convert UTC time to local time
                question['local_created_at'] = localtime(question['created_at'])

                # Generate a key to check if the question was liked/disliked by user
                q_key = ('questionmodel', question['question_id'])
                question['is_liked'] = q_key in liked_map
                question['is_disliked'] = q_key in disliked_map

                answer_list = []

                # Attach answers that belong to the current question
                for ans in answers:
                    if ans.get("question_id") == question.get("question_id"):
                        ans['local_created_at'] = localtime(ans['created_at'])

                        a_key = ('answermodel', ans['answer_id'])
                        ans['is_liked'] = a_key in liked_map
                        ans['is_disliked'] = a_key in disliked_map

                        answer_list.append(ans)

                # Append the structured question-answer block to the final list
                questions_list.append({
                    "question": question,
                    "answer": answer_list
                })

            # Render the dashboard page with the collected data
            return render(request, 'dashboard.html', context={
                "data": questions_list,
                "current_date": current_date
            })

        except Exception as e:
            # Return error as JSON if anything unexpected happens
            return JsonResponse({'error': f'Something went wrong: {str(e)}'}, status=500)


class PostQuestionView(LoginRequiredMixin, View):
    """
    Handles POST request to create a new question by the logged-in user.

    Expected POST data:
    - question_text: The text of the question being posted

    On success, redirects the user to the dashboard.
    """

    def post(self, request):
        try:
            # Extract the question text from the POST data
            question = request.POST.get('question_text')

            # Create a new QuestionModel entry associated with the current user
            QuestionModel.objects.create(
                user=request.user,   # The logged-in user posting the question
                question=question    # The actual question text
            )

            # Redirect to dashboard upon successful submission
            return redirect('dashboard')

        except Exception as e:
            # Catch-all for any unexpected errors during question posting
            return JsonResponse({'error': f'Something went wrong: {str(e)}'}, status=500)


class PostCommentView(LoginRequiredMixin, View):
    """
    Handles POST request to add a comment (answer) to a specific question.

    Expected POST data:
    - question-id: ID of the question being commented on
    - question-comment: The comment text

    On success, redirects the user to the dashboard.
    """

    def post(self, request):
        try:
            # Extract question ID from the POST data
            question_id = request.POST.get('question-id')

            # Extract comment text from the POST data
            comment = request.POST.get('question-comment')

            # Fetch the question instance using the given ID
            question_instance = QuestionModel.objects.get(question_id=int(question_id))

            # Create a new AnswerModel object (i.e., post the comment)
            AnswerModel.objects.create(
                user=request.user,            # Associate the comment with the current logged-in user
                question_id=question_instance,  # Link it to the fetched question instance
                answer=comment               # Set the comment text
            )

            # Redirect user to the dashboard on success
            return redirect('dashboard')

        except QuestionModel.DoesNotExist:
            # If the question ID doesn't match any existing question
            return JsonResponse({'error': 'Question not found'}, status=404)

        except (ValueError, TypeError):
            # In case of invalid question ID (not convertible to int, or missing)
            return JsonResponse({'error': 'Invalid question ID'}, status=400)

        except Exception as e:
            # Catch-all for any other unexpected errors
            return JsonResponse({'error': f'Something went wrong: {str(e)}'}, status=500)

    

class VoteView(LoginRequiredMixin, View):
    """
    Handles like/dislike votes on Questions and Answers.

    Expected GET parameters:
    - category: 'Q' for Question or 'A' for Answer
    - vote_type: 'Like' or 'Dislike'
    - id: object ID (question_id or answer_id)

    Returns:
    - JSON response with updated Like and Dislike count
    """

    def get(self, request):
        # Initialize the response with default like/dislike count as 0
        RESPONSE = {'LikeCount': 0, 'DisLikeCount': 0}

        # Get the category of content being voted on ('Q' for Question, 'A' for Answer)
        category = request.GET.get('category')

        # Get the type of vote ('Like' or 'Dislike')
        vote_type = request.GET.get('vote_type')

        # Get the object ID being voted on
        object_id = request.GET.get('id')

        # Validate all parameters are present and valid
        if not category or not object_id or vote_type not in ['Like', 'Dislike']:
            return JsonResponse({'error': 'Invalid parameters'}, status=400)

        # Try converting object ID to integer, return error if it fails
        try:
            object_id = int(object_id)
        except ValueError:
            return JsonResponse({'error': 'Invalid object ID'}, status=400)

        try:
            # Set the appropriate model and fields based on category
            if category == 'Q':
                model = QuestionModel  # Model for questions
                like_field = 'like_count'  # Field name for storing like count in QuestionModel
                dislike_field = 'dislike_count'  # Field name for storing dislike count
                # Fetch the question instance or return 404
                content_object = get_object_or_404(model, question_id=object_id)
            elif category == 'A':
                model = AnswerModel  # Model for answers
                like_field = 'like_count'
                dislike_field = 'dislike_count'
                # Fetch the answer instance or return 404
                content_object = get_object_or_404(model, answer_id=object_id)
            else:
                # If category is neither Q nor A, return error
                return JsonResponse({'error': 'Invalid category'}, status=400)

            # Get the content type for the selected model (used in generic foreign key)
            content_type = ContentType.objects.get_for_model(model)

            # Ensure operations are done in a transaction (all or nothing)
            with transaction.atomic():
                # Check if a vote from this user already exists for this object
                existing_vote = LikeModel.objects.filter(
                    user=request.user,
                    content_type=content_type,
                    object_id=object_id
                ).first()

                # If a vote already exists
                if existing_vote:
                    # If the same vote type is being applied again, user is retracting their vote
                    if existing_vote.vote_type == vote_type:
                        existing_vote.delete()  # Remove the vote record
                        if vote_type == 'Like':
                            # Decrease like count
                            setattr(content_object, like_field, getattr(content_object, like_field) - 1)
                        else:
                            # Decrease dislike count
                            setattr(content_object, dislike_field, getattr(content_object, dislike_field) - 1)
                    else:
                        # User is switching their vote from Like -> Dislike or vice versa
                        existing_vote.vote_type = vote_type  # Update vote type
                        existing_vote.save()  # Save changes to vote
                        if vote_type == 'Like':
                            # Increase like and decrease dislike count
                            setattr(content_object, like_field, getattr(content_object, like_field) + 1)
                            setattr(content_object, dislike_field, getattr(content_object, dislike_field) - 1)
                        else:
                            # Increase dislike and decrease like count
                            setattr(content_object, dislike_field, getattr(content_object, dislike_field) + 1)
                            setattr(content_object, like_field, getattr(content_object, like_field) - 1)
                else:
                    # If this is the first time user is voting on this object
                    LikeModel.objects.create(
                        user=request.user,  # Set current user
                        content_type=content_type,  # Content type of object
                        object_id=object_id,  # ID of the object being voted on
                        vote_type=vote_type  # Like or Dislike
                    )
                    # Increase like or dislike count depending on vote
                    if vote_type == 'Like':
                        setattr(content_object, like_field, getattr(content_object, like_field) + 1)
                    else:
                        setattr(content_object, dislike_field, getattr(content_object, dislike_field) + 1)

                # Save the updated like/dislike counts to the DB
                content_object.save(update_fields=[like_field, dislike_field])

                # Add updated counts to the response
                RESPONSE['LikeCount'] = getattr(content_object, like_field)
                RESPONSE['DisLikeCount'] = getattr(content_object, dislike_field)

            # Return JSON response with updated counts
            return JsonResponse(RESPONSE)

        except Exception as e:
            # Catch any unexpected exceptions and return error message
            return JsonResponse({'error': f'Something went wrong: {str(e)}'}, status=500)
