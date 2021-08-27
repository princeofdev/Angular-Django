import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams, AlertController, LoadingController } from 'ionic-angular';
import { FormBuilder, Validators, FormGroup } from '@angular/forms';

import { UIComponent } from '../../classes/component';

import * as moment from 'moment';
import { CardsService } from '../../providers/cards-service';
import { TranslateService } from '@ngx-translate/core'

@IonicPage()
@Component({
    selector: 'page-add-card',
    templateUrl: 'add-card.html',
})
export class AddCardPage extends UIComponent {

    private addCardForm: FormGroup;
    public showIcon: string;
    public translations: any      
    public title: string;
    public errorcard: string;
    minDate = null;
    maxDate = null;

    constructor(
      public navCtrl: NavController,
      public navParams: NavParams,
      private fb: FormBuilder,
      private cardsService: CardsService,
      private alertCtrl: AlertController,
      private loadingCtrl: LoadingController,
      public translateService: TranslateService      
    ) {
      super();
      this.addCardForm = this.fb.group({
          name: ["", Validators.required],
          cardnumber: ["", Validators.pattern(/^[0-9]{8,19}$/)],
          expiration: ["", Validators.required],
          cvc: ["", Validators.pattern(/^[0-9]{3}$/)]
      });
      this.translateService.get(['ADDCARD', 'CARDERROR', 'OK']).subscribe(values => {
        this.translations = values;
        this.title = values['ADDCARD'];
        this.errorcard = values['CARDERROR'];
      });
      this.setUIIdeal();
      this.minDate = moment().toISOString();
      this.maxDate = moment().add(10, "years").toISOString();
    }

    saveCard() {
      const expiration = this.addCardForm.value.expiration;
      const [year, month] = expiration.split("-");
      const card = {
        name: this.addCardForm.value.name,
        number: this.addCardForm.value.cardnumber,
        exp_month: month,
        exp_year: year,
        cvc: this.addCardForm.value.cvc
      };
      const loader = this.loadingCtrl.create();
      loader.present();
      this.cardsService.saveCard(card).subscribe(data => {
        loader.dismiss();this.navCtrl.pop();
      }, error => {
        loader.dismiss();
        this.alertCtrl.create({
          message: this.cardsService.errorToString(error), 
          buttons: [this.translations["OK"]]
        }).present();
      });
    }

}
