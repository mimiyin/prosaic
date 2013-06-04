function scroll(current, wordsies, callback) {
	//console.log("SCROLLING: " + wordsies.toString());
	// Size the animation div according to longest word
	var theWordsie = '#word' + current;
	
	var wordDiv = $('<div>').addClass('word').attr('id', 'word' + current);
	$('body').append(wordDiv);	
	
		
	// Figure out max font-size for this phrase
	var max = .08 * $(window).width();
	wordDiv.text(wordsies);
	wordDiv.css('font-size', 0);
	
	var width = $(window).width();
	var height = $(window).height();
	
	// Move the starting point of the animation
	wordDiv.css({
		'width'	: '100%',
		'float'	: 'left',
		'top'  : height-(height*.15),
		//'left' : 0,
		});
	
	//console.log(wordDiv);
	
	
	/* Delay the animation some arbitrary amount
	 * Set amount of time and velocity curve for text to grow
	 * Set amount of time and velocity curve for text to shrink
	 */
	wordDiv.delay(delay).animate({
		fontSize: max + 'px',
		}, wordsies.length*20 + 500, function(){ 
			callback();
			$(this).animate({
				//top: -100,
				fontSize: 0,
				opacity : 0,
			}, 5000, function(){
				$(this).remove();
			});
		});
	}

