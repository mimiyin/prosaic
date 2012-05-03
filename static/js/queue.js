function queueWrapper(path, callback, queryParameters) {
	var nextDelimiter = '?';
	// There's probably a library that handles this, eh?
	for ( var qp in queryParameters) {
		path += nextDelimiter + qp + '=' + queryParameters[qp];
		nextDelimiter = '&';
		}
	$.getJSON(path, function(data) {
		callback(data);
	});
};



// Get the data
var queue = {
		
	words : [],
	w : 0,
	y : 0,
	q_idx : 0,
	start_idx : 0,
	started : -1,
	timer : 0,
	
	reInit: function() {
		queue.words = [];
		queue.w = 0;
		queue.y = 0;
		queue.q_idx = 0;
		queue.start_idx = 0;
		queue.started = -1;
		queue.timer = 0;
		
		$(".word").stop();
		$(".word").fadeOut(5000);
	},
	
	getData: function() {
		console.log(queue.words);
		if (queue.q_idx > 9) queue.q_idx = 0;
		queueWrapper('queue', function(data){
			queue.words = data.words;
			// Cue Animation for "Testing 1,2,3"
			if(data.bookmark < 0) {
				queue.q_idx = 0;
				queue.start_idx = 0;
				queue.started = -1;
				queue.cueAnimation();
				}

			// At the start of the poem, get the bookmark and make that the start_idx
			else if(data.bookmark >= 0 && queue.started < 0) {
				console.log("STARTING");
				queue.start_idx = data.bookmark;
				queue.started = 1;
				queue.getData();
			}
			// Start the Poem Animation
			else if(queue.started > 0) {
				if(queue.words && queue.words.length > 0) {
					queue.cueAnimation();
					queue.q_idx++;			
					}
				 else {
					queue.timer = 0;
					queue.timer = setTimeout("queue.getData()", 5000);
					queue.w = 0;
					}
				}
			},
			{
				queue : queue.q_idx,
				start: queue.start_idx,
				started: queue.started
			});		
		},

	// Animate each word until there are none, get more data
	cueAnimation: function(){
		console.log(queue.w);
 		if (queue.w >= queue.words.length) {
 			queue.w = 0;
 			console.log("NEED MORE DATA: " + queue.w.toString());
 			queue.getData();
 			}
		else if(!hood) {
			console.log("ANIMATING WORDS");
			console.log(queue.words.length);
			var maxWords = queue.words.length;
			if(maxWords > 10) maxWords = 10;
			var numWords = parseInt(Math.random()*maxWords);
			var wordsToAnimate = [];
			var i = 0;
			while(i < numWords) {
				console.log("NUM WORDS: " + numWords.toString());
				console.log("WDX: " + queue.w.toString());
				console.log("IDX: " + i.toString());
				wordToAdd = queue.w-i;
				console.log("WORD TO ADD: " + wordToAdd.toString());
				if(wordToAdd > 1) wordsToAnimate.push(queue.words[wordToAdd-1]);
				else wordsToAnimate.push(queue.words[queue.w]);
				i++;
				} 	
			animate(wordsToAnimate, function() {
				queue.againAgain(true);});
	 		}
		else {
			console.log("SCROLLING");
			scroll(queue.w, queue.words[queue.w], function() {
				queue.againAgain(false)});
			}
	 	},
	 	
	 // Callback function that fetches more data when animation finishes	
	 againAgain: function(){
			queue.w++;
			console.log("CALLBACK " + queue.w.toString());
			queue.cueAnimation();
			},	
	};


