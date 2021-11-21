'use strict'

document.addEventListener('DOMContentLoaded', function(){
    const user_card = document.querySelector('.user_card');
    const get_user = document.querySelectorAll('.nav-link');
    const users = Array.from(get_user);

    const follow_btn = document.createElement('a');
    const i = document.createElement('i');

    follow_btn.classList.add("btn","btn-outline-primary", "follow_me");
    follow_btn.setAttribute('herf',"#");

    i.classList.add('bi','bi-eye','follow')
    i.innerHTML = "Follow";
    
    follow_btn.appendChild(i);

    if (user_card){
        if (user_card.firstElementChild.innerHTML != users[0].innerHTML){
            user_card.appendChild(follow_btn);
            console.log(user_card.firstElementChild.innerHTML,users[0].innerHTML);
        }
    }

})