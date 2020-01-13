document.addEventListener('click', function(event) {
  if (event.target.matches('#short')) {
    let shortDiv = document.getElementById('toShort')
    let outputDiv = document.getElementById('shortOutput')
    
    shortDiv.style.display = 'none'
    outputDiv.style.display = 'block'
    let url = document.getElementById('url').value
    fetch('/short', {
      method: 'POST',
      headers: {
        'content-type': 'application/json'
      },
      body: JSON.stringify({
        'url': url,
        'custom_name': ''
      })
    }).then(function(response) {
      return response.json()
    }).then(function(json) {
      if (json.hasOwnProperty('new_url')) {
        setValues('' + json['new_url'])
      } else {
        setValues(json['message'])
      }
    })
  } else if (event.target.matches('#back')) {
    let shortDiv = document.getElementById('toShort')
    let outputDiv = document.getElementById('shortOutput')
    shortDiv.style.display = 'block'
    outputDiv.style.display = 'none'
  }
}, false)

function setValues(message) {
  let outputP = document.getElementById('output')
  outputP.innerHTML = message
}