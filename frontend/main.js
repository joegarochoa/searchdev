let token = localStorage.getItem('token')
let loginButton = document.getElementById('login--button')
let buttonWrapper = document.getElementById("login--button")

loginButton.addEventListener('click', (e) => {
    e.preventDefault()
    
    //let buttonWrapper = document.getElementById("login--button")
    buttonWrapper.innerHTML = ''

    //let token = localStorage.getItem('token')
    console.log('Token: ', token)
    if (token){
        let buttonCard = `
            <a href="" id="login--button">Login</a>
        `    
        localStorage.removeItem('token')
        token = null
        console.log('Token1: ', token)
        buttonWrapper.innerHTML += buttonCard
    }else{
        let token = localStorage.getItem('token')
        console.log('Token0: ', token)
        let buttonCard = `
            <a href="" id="login--button">Logout</a>
        `    
        buttonWrapper.innerHTML += buttonCard
        window.location = 'file:///C:/Users/joegar/Desktop/try/frontend/login.html'
    }
})

let projectsUrl = 'http://127.0.0.1:8000/api/projects/'

let getProjects = () => {

    fetch(projectsUrl) 
        .then(response => response.json())
        .then(data => {
            buildProjects(data)
        })
}

let buildProjects = (projects) => {
    let buttonWrapper = document.getElementById("login--button")
    buttonWrapper.innerHTML = ''
    //let token = localStorage.getItem('token')
    console.log('Token:2a ', token)

    //dateString = object.timestamp,
    //now = new Date().getTime().toString();
    //compareTime(dateString, now); //to implement

    if (token){
        let buttonCard = `
            <a href="" id="login--button">Logout</a>
        `    
        buttonWrapper.innerHTML += buttonCard
    }else{
        let buttonCard = `
            <a href="" id="login--button">Login</a>
        `    
        buttonWrapper.innerHTML += buttonCard
    }

    let projectsWrapper = document.getElementById("projects--wrapper")
    projectsWrapper.innerHTML = ''

    for (let i = 0; projects.length > i; i++) {
        let project = projects[i]
        let projectCard = `
            <div class="project--card">
                <img src="http://127.0.0.1:8000${project.featured_image}">
                
                <div>
                    <div class="card--header">
                        <h3>${project.title}</h3>
                        <strong class="vote--option" data-vote="up" data-project=${project.id}>&#43;</strong>
                        <strong class="vote--option" data-vote="down" data-project=${project.id}>&#8722;</strong>
                    </div>
                    <i>${project.vote_ratio}% Positive Feedback</i>
                    <p>${project.description.substring(0,150)}</p>

                </div>
            </div>
        `
        projectsWrapper.innerHTML += projectCard
    }
    
    addVoteEvents()

}

let addVoteEvents = () => {
    //let token = localStorage.getItem('token')
    console.log('Token2: ', token)
    let voteButtons = document.getElementsByClassName('vote--option')

    for (let i = 0; voteButtons.length > i; i++) {

        voteButtons[i].addEventListener('click', (e) => {
            if (token){
                console.log('Token3: ', token)
                let vote = e.target.dataset.vote
                let project = e.target.dataset.project

                fetch(`http://127.0.0.1:8000/api/projects/${project}/vote/`, {
                    method:'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({'value': vote})
                })
                    .then(response => {
                        if (response.ok) {
                            response.json()
                            .then(data => {
                                console.log(data)
                                getProjects()        
                            })
                        }
                        else if (response.status = 401) {
                            localStorage.removeItem('token')
                            buttonWrapper.innerHTML = ''
                            let buttonCard = `
                                <a href="" id="login--button">Login</a>
                            `    
                            buttonWrapper.innerHTML += buttonCard
                            alert('Required Authorization not found/expired.')
                        }
                    })
            }else{
                alert('Required Authorization not found/expired.')
            }
        })
    }
}

getProjects()

// source of html arrow - toptal.com/designers/htmlarrows/
