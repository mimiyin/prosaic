var rgrow = 0, 
	rshrink = 0, 
	rdelay = 0,
	rmax = 10000;

var easingOpts = ['linear', 'swing', 'easeInQuad', 'easeOutQuad', 'easeInOutQuad', 'easeInCubic', 'easeInOutCubic', 'easeInQuart', 'easeOutQuart',
                  'easeInOutQuart', 'easeInQuint', 'easeOutQuint', 'easeInOutQuint', 'easeInSine', 'easeOutSine', 'easeInOutSine', 'easeInExpo',
                  'easeOutExpo', 'easeInOutExpo', 'easeInCirc', 'easeOutCirc', 'easeInOutCirc', 'easeInElastic', 'easeOutElastic', 'easeInBack',
                  'easeInOutBack', 'easeInBounce', 'easeOutBounce', 'easeInOutBounce'];

var easingCount = easingOpts.length-1;

function grow(numWords){
		rgrow += Math.random()*10;
		var dividend = 50*numWords;
		var growth = dividend/Math.abs(Math.sin(Math.tan(rgrow)));
		//if(growth > rmax) growth = rmax;
		return growth;
	}

function shrink(numWords) {
		rshrink += Math.random()*10;
		var dividend = 50*numWords;
		var diminution = dividend/Math.abs(Math.cos(Math.tan(rshrink)));
		//if(diminution > rmax) diminution = rmax;
		return diminution;	
	}
	
function delay(){
		rdelay += Math.random();
		return Math.abs(Math.cos(rdelay))*100;
	}
	  
function animate(wordsToAnimate, callback) {
	console.log("THE WORDS: " + wordsToAnimate.toString());
	if(wordsToAnimate != undefined && wordsToAnimate.length > 0) {
		//console.log(thisWord);
		//console.log(prevWord);

		var mult = wordsToAnimate[0].length;
		var grew = grow(mult);
		var shrunk = shrink(mult);
		var deelay = delay(mult);
				
		//console.log(grew + '\t' + shrunk + '\t' + deelay);
		
		// Flip a coin
		var animateMany = Math.random()*wordsToAnimate.length;
		$.each(wordsToAnimate, function(i, wordToAnimate){
			console.log("ANIMATE MANY: " + i + "\t" + animateMany.toString());
			if(i < animateMany-1) doIt(0, wordToAnimate, grew, shrunk, deelay);
			else if(i < animateMany) doIt(2, wordToAnimate, grew, shrunk, deelay, callback);
			});
	}
	else {
		//console.log("NOTHING");
		callback();
	}
}

function doIt(current, theWord, grow, shrink, delay, callback) {
	// Split data into array of words
	var wordsies = theWord.split(' ');
	var numWords = wordsies.length;
//	var longestWord = '';
//	var longestLength = 0;
//	
//	// Find the longest word
//	$.each(wordsies, function(w, wordsie){
//		if(wordsie.length > longestLength) {
//			longestLength = wordsie.length;
//			longestWord = wordsie;
//			}		
//		});
		
	// Size the animation div according to longest word
	var theWordsie = '#word' + current;
	//console.log(theWordsie);
	//console.log(theWord);
	
	var wordDiv = $('<div>').addClass('word').attr('id', 'word' + current);
	$('body').append(wordDiv);	
	//wordDiv.text(longestWord);
	
	
	// Figure out max font-size for this phrase
	var max = parseInt(Math.random()*1000) + 200;//resizeText(wordDiv);
	wordDiv.empty();
	wordDiv.css('font-size', 0);
	
	var width = $(window).width();
	var height = $(window).height();
	
	// Move the starting point of the animation
	wordDiv.css({
		'left' : (Math.random()*width) - width/2,
		'top'  : (Math.random()*height*.75) - height/5,	
		});
	
	//console.log(wordDiv);
	
	// Calculate rate at which words change during animation
	var wdx = 0;
	var stepMult = .75;
	var stepTH = (max*stepMult)/numWords;
	
	/* Delay the animation some arbitrary amount
	 * Set amount of time and velocity curve for text to grow
	 * Set amount of time and velocity curve for text to shrink
	 */
	wordDiv.delay(delay).animate({
		fontSize: max + 'px',
		},
	{
	    duration: grow,
	    easing: easingOpts[Math.floor(Math.random()*easingCount)],
	    step: function(now, fx) {
	    	var TH = stepTH*wdx + max*(1-stepMult);
	    	if(now > TH) {
	    		var nextWord = wordsies[wdx];
	    		wordDiv.text(nextWord);
	    		wdx++;
	    		}
	    	},
	    complete: function(){
	    	wdx = 0;
	    	wordDiv.delay(delay).animate({
				fontSize: '0px',
				}, 
				{
				    duration: shrink,
				    easing: easingOpts[Math.floor(Math.random()*easingCount)],
				    step: function(now, fx) {
				    	var TH = max*stepMult - stepTH*wdx;
				    	if(now < TH) {
				    		var nextWord = wordsies[(numWords-1)-wdx];
				    		wordDiv.text(nextWord);
				    		wdx++;
					  		}
				    	},
				    complete: callback,
				}); 
	    	},
		});
	}

//Dynamically resize flag text in reading list to fill up the space
function resizeText(wordDiv) {
    var width = wordDiv.width(),
        html = '<p class=resizedText></p>',
        line = wordDiv.wrapInner( html ).children()[ 0 ],
        n = 500;
    wordDiv.css( 'font-size', n );

    while ( $( line ).width() > width ) {

        wordDiv.css( 'font-size', --n );
    }
    
    wordDiv.html( $( line ).html() );
    
    return n;
}
