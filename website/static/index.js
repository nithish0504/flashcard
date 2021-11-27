function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
function hello(){
  console.log("hello here")
  deckName = prompt("Create new deck with name:");
}


function editDeck(deckId) {

  deckName = prompt("Enter the new name:");
  if(deckName !== null){
    if(deckName !== ""){
      if(deckName.length<2){
        alert("Deck Name Too Short")
        return
      }
    }else{
      alert("Please Enter Deck Name")
      return
    }
  }else{
    return
  }

  fetch("/", {
    method: "PUT",
    body: JSON.stringify({ deckName: deckName, deckId:deckId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function deleteDeck(deckId) {
  fetch("/delete-deck", {
    method: "POST",
    body: JSON.stringify({ deckId: deckId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
function deleteCard(cardId) {
  fetch("/delete-card", {
    method: "POST",
    body: JSON.stringify({ cardId: cardId }),
  }).then((_res) => {
    window.location.href = "/deck/";
  });
}