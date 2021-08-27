import { Component,Input,Output, EventEmitter} from '@angular/core';


/**
 * Generated class for the CalendarComponent component.
 *
 * See https://angular.io/api/core/Component for more info on Angular
 * Components.
 */
@Component({
  selector: 'calendar',
  templateUrl: 'calendar.html'
})
export class CalendarComponent {

  @Input() title: string;
  @Input() date: any;
  @Input() options: any;
  @Input() type;
  @Input() format;

  @Output() onChange: EventEmitter<any> = new EventEmitter<any>();

  constructor(
  ) {

  }

  changeDay(event){
    this.onChange.emit(event);
  }

}
