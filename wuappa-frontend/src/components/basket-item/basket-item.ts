import { Component,Input, Output, EventEmitter } from '@angular/core';


@Component({
  selector: 'basket-item',
  templateUrl: 'basket-item.html'
})
export class BasketItemComponent {

  text: string;
  @Input() item;

  @Output() increment: EventEmitter<any> = new EventEmitter<any>();
  @Output() decrement: EventEmitter<any> = new EventEmitter<any>();

  constructor() {
  }



  incrementService(){    
    this.increment.emit(this.item.id);
  }

  decrementService(){
    this.decrement.emit(this.item.id);
  }

}
