//given object
const ChatClient = {
    sendMessage: function(messageText) {...},
    onReceiveMessage: function(callback) {...}
}


//dictionary for words to be stored
var wordCache = {};

// sort words in dictionary and return the top 10 words in an array
function findTop10(){
  //create array of words and their number of times used
  var words = Object.keys(wordCache).map(function(key) {
    return [key, wordCache[key]];
  });

  // Sort the array based on the second element, which is their times used
  words.sort(function(first, second) {
      return second[1] - first[1];
  });

  //reset the dictionary for the next interval
  wordCache = {};

  // pass the top 10 words in an array to the function that will return a string containing the top 10 words and then return that.
  return messageBuilder(words.slice(0, 10));

}

//construct a message with the top 10 words in decreasing word count
function messageBuilder(wordsArray){
  //the array will look like this from the other function: [ [ 'the', 17 ], [ 'cat', 11 ], [ 'in', 9 ], [ 'hat', 7 ], [ 'foo', 6 ],... ]
  message = "Here are the top 10 most common words used by the room. ";
  wordsArray.forEach(function(word){
    message = message + word[0] + ": Used " + word[1] + " times. ";
  });
  return message;
}

// take the received message, split [username] from [messageText], then split messageText in to words and store them in a dictionary with the word being the key and the value being the times it was seen.
function wordCounter(chatInput){
  //split the input on ": " and grab only the part we care about. We assume there will be no username allowed with ": " in it so it always seperates the username from the message.
  var message = chatInput.split(": "[1]);
  //now we split on " " to get an array of words.
  words = message.split(" ");
  //parse each word to see if the word contains non alphanumerics, if so, remove them, then save it to the dictionary or increase its count if it has been used already.
  words.forEach(function(word){
    word = word.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"");
    if (word in wordCache){
      wordCache[word]++;
    } else {
      wordCache[word] = 1;
    }
  });
}

// set an interval to send a message every 5 min. 5*60*1000 = 300000ms = 5 min
setInterval(function(){
    ChatClient.sendMessage(findTop10());
}, 300000);


//register wordCounter as the function to run after a message comes in.  Assuming it uses the wordCounter as its callback after a message has been recieved.
ChatClient.onReceiveMessage(wordCounter);
