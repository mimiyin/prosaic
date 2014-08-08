function queueWrapper(path, callback, queryParameters) {
	var nextDelimiter = '?';
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
	subQ: -1,
	preQ: -1,
	
	reInit: function(subQ, preQ) {
		queue.words = [];
		queue.w = 0;
		queue.y = 0;
		queue.q_idx = 0;
		queue.start_idx = 0;
		queue.started = -1;
		queue.timer = 0;
		queue.subQ = subQ;
		queue.preQ = preQ;
		
		$(".word").stop();
		$(".word").fadeOut(5000);
	},
	
	getData: function(name) {
		queue.name = name || queue.name;
		//console.log("PreQ: " + queue.preQ.toString());		
		
		//console.log(queue.words);
		if (queue.q_idx > 9) queue.q_idx = 0;
		
		queueWrapper('queue', function(data){
			console.log(data);
			queue.words = data.words;
			console.log(queue.words[0]);

			if(new RegExp('up').test(queue.words[0]) && !crazy) {
				queue.words.splice(0,0,'');
				queue.words.splice(0, 0,'go');
				for(var i= 0; i < 7; i++) {
					queue.words.splice(0,0,'');
				}
				for(var i= 0; i < 15; i++) {
					var text = Math.random() > .5 ? 'ready' : 'get set';
					queue.words.splice(0, 0, text);
				}

				for(var i= 0; i < 40; i++) {
					queue.words.splice(0,0,'');
				}

				$("<div>").appendTo("body").addClass("word").text("[ Read me. ]").hide().fadeIn(15000, function(){
					$(this).fadeOut(5000);
				})
			}

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
				queue.getData(queue.subQ, queue.preQ);
			}
			// Start the Poem Animation
			else if(queue.started > 0) {
				if(queue.words && queue.words.length > 0) {
					queue.cueAnimation();
					queue.q_idx++;			
					}
				 else {
					queue.timer = 0;
					queue.timer = setTimeout( function(){ queue.getData(subQ) }, 5000);
					queue.w = 0;
					}
				}
			},
			{
				name: queue.name,
				queue : queue.q_idx,
				start: queue.start_idx,
				started: queue.started,
				subQ: queue.subQ,
				preQ: queue.preQ,
				mode: crazy ? "1" : "0",
			});		
		},

	// Animate each word until there are none, get more data
	cueAnimation: function(){
		//console.log(queue.w);
 		if (queue.w >= queue.words.length) {
 			queue.w = 0;
 			if(queue.name) {
	 			console.log("NO NEED FOR MORE DATA!!!");
 				queue.cueAnimation();
 			}
 			else {
	 			console.log("NEED MORE DATA: " + queue.w.toString());
				console.log("THE END");
	 			setTimeout(function() { queue.getData() }, 5000);
 			}
 		}
		else if(!hood) {
			console.log("ANIMATING " + queue.words.length +" WORDS");
			var maxWords = queue.words.length;
			if(maxWords > 10) maxWords = 10;
			var numWords = parseInt(Math.random()*maxWords);
			var wordsToAnimate = [];
			var i = 0;
			while(i < numWords) {
				//console.log("NUM WORDS: " + numWords.toString());
				//console.log("WDX: " + queue.w.toString());
				//console.log("IDX: " + i.toString());
				wordToAdd = queue.w-i;
				//console.log("WORD TO ADD: " + wordToAdd.toString());
				if(wordToAdd > 1) wordsToAnimate.push(queue.words[wordToAdd-1]);
				else wordsToAnimate.push(queue.words[queue.w]);
				i++;
				} 	
			animate(wordsToAnimate, function() {
				queue.againAgain(true);});
	 		}
		else {
			//console.log("SCROLLING");
			scroll(queue.w, queue.words[queue.w], function() {
				queue.againAgain(false)
				});
			}
	 	},
	 	
	 // Callback function that fetches more data when animation finishes	
	 againAgain: function(){
			queue.w++;
			//console.log("CALLBACK " + queue.w.toString());
			queue.cueAnimation();
			},	
	};


