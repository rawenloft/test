document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#send-mail').addEventListener('click', send_mail);
  
  // By default, load the inbox
  load_mailbox('inbox');
  document.querySelector('#emails-view').classList.add('container');

});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  // Show emails
  fetch(`/emails/${mailbox}`).then(response => response.json()).then(emails => {
    open_mail(emails);
    emails.forEach(email => {
      make_email(email);
    })
  })
  
}

function send_mail(){
  fetch('/emails', {
    method: "POST",
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject:document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
    })
  }).then(response => response.json()).then(result => {
    console.log(result);
  });
  return false;
}

function make_email(email){
  const mail_elem = document.createElement('div');
  const sender = document.createElement('span');
  const subj = document.createElement('span');
  const timestamp = document.createElement('span');

  mail_elem.classList.add('row','mail','rounded','read');
  sender.classList.add('col-lg-2','col-sm-6');
  subj.classList.add('col-lg-7','col-sm-6');
  timestamp.classList.add('col-lg-3','col-sm-12');

  sender.innerHTML = email.sender;
  subj.innerHTML = email.subject;
  timestamp.innerHTML = email.timestamp;

  mail_elem.append(sender)
  mail_elem.append(subj)
  mail_elem.append(timestamp)

  mail_elem.addEventListener('click', () => {
    console.table(email)
  });
  document.querySelector('#emails-view').append(mail_elem);
}

function open_mail(emails){
  return
}