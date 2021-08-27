import { Component, Input } from '@angular/core';
import { OnInit } from '@angular/core/src/metadata/lifecycle_hooks';

@Component({
  selector: 'service-card',
  templateUrl: 'service-card.html'
})
export class ServiceCardComponent implements OnInit {

  @Input() service: any;
  @Input() prueba: string;
  price: any = "";
  price_currency: any = "";

  constructor(
  ) {
  }
  ngOnInit() {
    this.checkCity();
  }


  checkCity(){
    if(this.service.cities.length != 0){

        if(typeof(this.service.cities[0].price ) !== 'undefined'
        && typeof(this.service.cities[0].price_currency !== 'undefined')){

          this.price = this.service.cities[0].price;
          this.price_currency = this.service.cities[0].price_currency;
        }
    }
  }

  getImage(){
    let serviceHasImage = this.service.image != null ;
    let myStyles = {
      'background-image': (serviceHasImage) ? 'url(' + this.service.image + ')' : 'none',
      'background-color': (!serviceHasImage) ? 'grey': 'none'
    }

    return myStyles;
  }

}
