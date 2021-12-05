'use strict'

window.addEventListener('DOMContentLoaded', ()=>{
    const menu = document.querySelector('.new_post');
    let flag = false;
    let lines = document.querySelectorAll('.line');
    const newPost = document.querySelector('.new_post--form')
    const editPost = document.querySelector('.edit_post')

    function menuChange(){
        if (!flag){
            lines[0].style.transform = "rotate(45deg) translateY(5px)";
            lines[0].style.transition = "all .3s";
            lines[1].style.display = "none";
            lines[2].style.transform = "rotate(-45deg) translateY(-5px)";
            lines[2].style.transition = "all .3s";
            flag = !flag;
        } else {
            flag = !flag;
            lines[0].style.transform = "rotate(0) translateY(0)";
            lines[0].style.transition = "all .3s";
            lines[1].style.display = "block";
            lines[2].style.transform = "rotate(0) translateY(0)";
            lines[2].style.transition = "all .3s";

        }
    }
    function show_form(){
        if (flag){
            newPost.style.display = "none";
            newPost.style.transition = "all .3s"
        } else {
            newPost.style.display = "block";
            newPost.style.transition = "all .3s"
        }
    }
    if (menu) {
        menu.addEventListener('click', ()=> {
            show_form();
            menuChange();
        })
    }
    if (editPost){

        editPost.addEventListener('click', (e) => {
            e.preventDefault();
            let text = e.target.parentElement.firstChild.nextSibling;
    
            let newPost = newPostForm(text)
            
            console.log(newPost);
            newPost.style.display = "block";
    
            e.target.parentElement.insertBefore(newPost, text)
            // text.parentElement.appendChild(newPost);
            text.remove()
            e.target.remove()
        })
        function newPostForm(text){
            let postForm = document.querySelector('.post_form').cloneNode(true);
            postForm.firstChild.nextSibling.nextSibling.nextSibling.firstChild.nextSibling.innerHTML = 'Update post';
            postForm.firstChild.nextSibling.nextSibling.nextSibling.firstChild.nextSibling.nextSibling.nextSibling.value = text.innerHTML;
            postForm.firstChild.nextSibling.nextSibling.nextSibling.classList.remove('new_form')
            return postForm
        }
    }
})