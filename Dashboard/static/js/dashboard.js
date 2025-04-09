const colors = ['#FF5733', '#33FF57', '#3357FF', '#F3FF33', '#FF33A1'];

function getRandomColor() {
    const randomIndex = Math.floor(Math.random() * colors.length);
    return colors[randomIndex];
}

const randomColor = getRandomColor();
document.documentElement.style.setProperty('--global-bg-color', randomColor);


window.onclick = function(event) {
    const modal = document.getElementById("questionModal");
    if (event.target == modal) {
        closeModal();
    }
}


function changeModalTab(e){
    const id = e.id;
    if(id == "add-question"){
        document.getElementById("post-modal").style.display = "None";
        document.getElementById("question-modal").style.display = "block";
    }else{
        document.getElementById("post-modal").style.display = "block";
        document.getElementById("question-modal").style.display = "None";
    }
}

function opencomment(e) {
    const commentBox = document.getElementById(`question-comment-${e.id}`);
    const displayValue = window.getComputedStyle(commentBox).display;

    if (displayValue == 'none'){
        document.getElementById(`question-comment-${e.id}`).style.display = "block";
    }
    else{
        document.getElementById(`question-comment-${e.id}`).style.display = "None";
    }
}


function questionLikeDisLike(category,id){

    if(category=='Like'){

        fetch(`like-dislike-question-answer?id=${id}&category=Q&vote_type=Like`)
        .then(response => {
            if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json()
        })
        .then(data => {

            document.getElementById(`question-dislike-${id}`).style.color = document.getElementById(`question-dislike-${id}`).style.color === "rgb(40, 125, 255)" ? 'white' : "rgb(40, 125, 255)";
            document.getElementById(`question-like-${id}`).style.color = document.getElementById(`question-like-${id}`).style.color === "rgb(40, 125, 255)" ? 'white' : "rgb(40, 125, 255)";
            document.getElementById(`question-dislike-${id}-span`).innerText =  data['DisLikeCount']
            document.getElementById(`question-like-${id}-span`).innerText =  data['LikeCount']
        }
        )
        .catch(error => {
            console.error('Error:', error);
        });
    

    }
    else{
        
        fetch(`like-dislike-question-answer?id=${id}&category=Q&vote_type=Dislike`)
        .then(response => {
            if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json()
        })
        .then(data => {
            document.getElementById(`question-dislike-${id}`).style.color = document.getElementById(`question-dislike-${id}`).style.color === "rgb(40, 125, 255)" ? 'white' : "rgb(40, 125, 255)";
            document.getElementById(`question-like-${id}`).style.color = document.getElementById(`question-like-${id}`).style.color === "rgb(40, 125, 255)" ? 'white' : "rgb(40, 125, 255)";

            document.getElementById(`question-dislike-${id}-span`).innerText =  data['DisLikeCount']
            document.getElementById(`question-like-${id}-span`).innerText =  data['LikeCount']
        }
        )
        .catch(error => {
            console.error('Error:', error);
        });
        
    }
    
}



function answerLikeDisLike(category,id){

    if(category=='Like'){

        fetch(`like-dislike-question-answer?id=${id}&category=A&vote_type=Like`)
        .then(response => {
            if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json()
        })
        .then(data => {

            document.getElementById(`answer-dislike-${id}`).style.color = document.getElementById(`answer-dislike-${id}`).style.color === "rgb(40, 125, 255)" ? 'white' : "rgb(40, 125, 255)";
            document.getElementById(`answer-like-${id}`).style.color = document.getElementById(`answer-like-${id}`).style.color === "rgb(40, 125, 255)" ? 'white' : "rgb(40, 125, 255)";
            document.getElementById(`answer-dislike-${id}-span`).innerText =  data['DisLikeCount']
            document.getElementById(`answer-like-${id}-span`).innerText =  data['LikeCount']
        }
        )
        .catch(error => {
            console.error('Error:', error);
        });
    

    }
    else{
        
        fetch(`like-dislike-question-answer?id=${id}&category=A&vote_type=Dislike`)
        .then(response => {
            if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json()
        })
        .then(data => {
            document.getElementById(`answer-dislike-${id}`).style.color = document.getElementById(`answer-dislike-${id}`).style.color === "rgb(40, 125, 255)" ? 'white' : "rgb(40, 125, 255)";
            document.getElementById(`answer-like-${id}`).style.color = document.getElementById(`answer-like-${id}`).style.color === "rgb(40, 125, 255)" ? 'white' : "rgb(40, 125, 255)";
            document.getElementById(`answer-dislike-${id}-span`).innerText =  data['DisLikeCount']
            document.getElementById(`answer-like-${id}-span`).innerText =  data['LikeCount']
        }
        )
        .catch(error => {
            console.error('Error:', error);
        });
        
    }
    
}
