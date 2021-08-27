import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';


@Component({
  selector: 'punctuation-stars',
  templateUrl: 'punctuation-stars.html'
})
export class PunctuationStarsComponent implements OnInit{
  @Input() read: boolean;
	@Input() punctuation;
	@Input() numStars: number = 5;
	@Input() value: number;
	@Input() scale: number = 1;

	@Output() clicked: EventEmitter<number> = new EventEmitter<number>() ;

	stars: string[] = [];
	 
  constructor() {

	}
	
  ngOnInit() {
			this.calcStars();
	}


  calcStars(){
  	this.stars = [];
	  let punctuation = Math.round(this.value / this.scale);
    
	  for (let i = 0; i < this.numStars; i++, punctuation--) {
			if(punctuation >= 1)
			  this.stars.push("star");
		  else if (punctuation < 1 && punctuation > 0)
			  this.stars.push("star-half");
		  else
			  this.stars.push("star-outline");
		}
		 
  }

  starClicked(index){
			this.calcStars();
			if(!this.read) {
				this.value = index + 1;
				this.calcStars();
				this.clicked.emit(this.value);
			}
  }
}
