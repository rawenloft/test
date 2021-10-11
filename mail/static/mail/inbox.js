document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#send-mail').addEventListener('click', send_mail);
  
  // By default, load the inbox
  const last_mailbox = localStorage.getItem('last_mailbox');
  (last_mailbox == '' || last_mailbox != 'sent') ? load_mailbox('inbox') : load_mailbox(last_mailbox);
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
    emails.forEach(email => {
      list_email(email);
    })
  })
  // Clearing messages from all other mailboxes
  const last_mail = document.querySelector('#mail-view');
  if (last_mail) {
    last_mail.remove()
  }
  // Update local storage
  localStorage.setItem('last_mailbox', mailbox);
}

// Sending mail
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
  localStorage.setItem('last_mailbox', 'sent');
  return false;
}
// Creating list of mails in mailbox
function list_email(email){
  const mail_elem = document.createElement('div');
  const sender = document.createElement('span');
  const subj = document.createElement('span');
  const timestamp = document.createElement('span');

  mail_elem.classList.add('row','mail','rounded');
  sender.classList.add('col-lg-2','col-sm-6');
  subj.classList.add('col-lg-7','col-sm-6');
  timestamp.classList.add('col-lg-3','col-sm-12');

  if (email.read){
    mail_elem.classList.add('read');
    mail_elem.classList.remove('unread');     
  } else {
    mail_elem.classList.remove('read');
    mail_elem.classList.add('unread');
  }

  sender.innerHTML = email.sender;
  subj.innerHTML = email.subject;
  timestamp.innerHTML = email.timestamp;

  mail_elem.append(sender);
  mail_elem.append(subj);
  mail_elem.append(timestamp);

  mail_elem.addEventListener('click', () => {
    show_mail(email)
    read_message(email);
    // console.table(email);
  });
  
  document.querySelector('#emails-view').append(mail_elem);
  
}
// Composing opened mail
function open_mail(email){
  
  const mail = document.createElement('div');
  const mail_sender = document.createElement('div');
  const mail_receiver = document.createElement('div');
  const mail_subject = document.createElement('div');
  const mail_timestamp = document.createElement('div');
  const reply_button = document.createElement('button');
  const hr = document.createElement('hr');
  const mail_text = document.createElement('div');
  const user = document.querySelector('h2').innerHTML;


  reply_button.setAttribute('id','reply');
  reply_button.classList.add('btn','btn-sm','btn-outline-primary');

  mail_timestamp.innerHTML = "<b>From: </b>" + email.sender;
  mail_subject.innerHTML = "<b>To: </b>" + email.recipients;
  mail_sender.innerHTML = "<b>Subject: </b>" +  email.subject;
  mail_receiver.innerHTML = "<b>Timestamp: </b>" + email.timestamp;
  reply_button.innerHTML = "Reply";
  mail_text.innerHTML = email.body;

  mail.setAttribute('id','mail-view');

  mail.append(mail_timestamp);
  mail.append(mail_subject);
  mail.append(mail_receiver);
  mail.append(mail_sender);

  if (user != email.sender){
    reply_button.addEventListener('click', () => {
      reply_this(email);
    });
    mail.append(reply_button);
  }
// Composing archive button with label
  if (email.read && user != email.sender){
    const archive_button = document.createElement('i');
    const archive_label = document.createElement('span');

    archive_button.addEventListener('click',() => {
      message_status(email);
    })
    archive_label.addEventListener('click',() => {
      message_status(email);
    })

    archive_button.classList.add('far','fa-bookmark','icon');
    archive_label.classList.add('icon-label');
    archive_label.innerHTML = 'Archive';

    mail.append(archive_button);
    mail.append(archive_label);

    if (email.archived){
      archive_button.classList.remove('far');
      archive_button.classList.add('fas');
  
      archive_label.innerHTML = 'Unarchive';

    } 
  }

  mail.append(hr);
  mail.append(mail_text);

  return mail
}

// Showing single mail
function show_mail(email){
  
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  // console.log(document.querySelector('#compose-view').parentElement.lastChild);
  if (document.querySelector('#emails-view').parentElement.contains(document.querySelector('#mail-view'))){
    document.querySelector('#mail-view').remove()
    document.querySelector('#emails-view').parentElement.appendChild(open_mail(email));

  } else {
    document.querySelector('#emails-view').parentElement.appendChild(open_mail(email));
  }
  
}
// Reply message composing
function reply_this(email){
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#mail-view').remove();

  document.querySelector('#compose-recipients').value = email.sender;
  document.querySelector('#compose-subject').value = subject_check(email);
  document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: "${email.body}"` + '\n\t';
}
// Checking subject for replying message
function subject_check(email){
  const original_subject = email.subject;
  let subject = '';
  if (original_subject.substring(0,4) === "Re: "){
    return subject = original_subject;
  }
  return subject = "Re: " + email.subject;
}
// Updating status of messages
function read_message(email){
  if (!email.read){
    fetch(`/emails/${email.id}`,{
      method: 'PUT',
      body: JSON.stringify({
        read: !email.read,
      })
    })
  }
}
// Change status of archived message
function message_status(email){
  fetch(`/emails/${email.id}`,{
    method: 'PUT',
    body: JSON.stringify({
      archived: !email.archived,
    })
  })
  load_mailbox('inbox');
}