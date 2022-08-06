document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function send_email() {

  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      if("message" in result){
        alert(result.message);
      }
      else{
        alert(result[error]);
      }
  })

  load_mailbox('sent');
  return false;
}

function reply_email(email) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#content-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  document.querySelector('#compose-recipients').value = email.sender;
  document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
  document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
}

function archive_email(email_id, archive) {
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !archive
    })
  });
  document.location.reload();
}

function view_email(email_id) {

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#content-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  //document.getElementById('#content-view').textContent = '';
 

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);

    const email_content = document.querySelector('#content-view');
    email_content.innerHTML = "";

    const sender = document.createElement('div');
    sender.innerHTML = 'From: '.bold() + email.sender;
    email_content.appendChild(sender);

    const recipient = document.createElement('div');
    recipient.innerHTML = 'To: '.bold() + email.recipients[0];
    email_content.appendChild(recipient);

    const subject = document.createElement('div');
    subject.innerHTML = 'Subject: '.bold() + email.subject;
    email_content.appendChild(subject);

    const timestamp = document.createElement('div');
    timestamp.innerHTML = 'Timestamp: '.bold() + email.timestamp;
    email_content.appendChild(timestamp);

    const reply = document.createElement('button');
    reply.id = "reply";
    reply.className = 'btn btn-outline-primary';
    reply.innerText = 'Reply';
    email_content.appendChild(reply);

    const archive = document.createElement('button');
    archive.id = 'archive';
    archive.className = 'btn btn-outline-primary';
    if (email.archived === false) {
      archive.innerText = 'Archive';
    }
    else{
      archive.innerText = 'Unarchive';
    }
    
    email_content.appendChild(archive);
    

    const hr = document.createElement('hr');
    email_content.appendChild(hr);

    const body = document.createElement('div');
    body.innerHTML = email.body;
    email_content.appendChild(body);

    document.querySelector('#archive').addEventListener('click', () => archive_email(email_id, email.archived));
    reply.addEventListener('click', () => reply_email(email));
   
  })

  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })

  
}

function show_email(mailbox, email) {

  const element = document.createElement('div');
  element.id = "email";
  element.className = "container";

  const recipient = document.createElement('div');
  recipient.id = "email-recipient";
  if (mailbox === 'sent') {
    recipient.innerHTML = email.recipients[0];
  }
  else {
    recipient.innerHTML = email.sender;
  }
  element.append(recipient);

  const subject = document.createElement('div');
  subject.id = "email-subject";
  subject.innerHTML = email.subject;
  element.append(subject);

  const timestamp = document.createElement('div');
  timestamp.id = "email-timestamp";
  timestamp.innerHTML = email.timestamp;
  element.append(timestamp);

  if (email.read === false){
    element.style.backgroundColor = "white";
  } else{
    element.style.backgroundColor = "#D3D3D3";
  }
  document.querySelector('#emails-view').append(element);
  
  element.addEventListener('click', () => view_email(email.id));

}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#content-view').style.display = 'none';
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
  document.querySelector('#content-view').style.display = 'none';
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);
      emails.forEach(email => {
        show_email(mailbox, email);
      });
    });
  
  localStorage.clear();
      // ... do something else with emails ...
}