import { Component } from '@angular/core';
import { IonicPage, NavController, AlertController, LoadingController, NavParams, ViewController } from 'ionic-angular';
import { AddCardPage } from '../add-card/add-card';
import { UIComponent } from '../../classes/component';
import { CardsService } from '../../providers/cards-service';
import { TranslateService } from '@ngx-translate/core';


@IonicPage()
@Component({
    selector: 'page-payment-method',
    templateUrl: 'payment-method.html',
})
export class PaymentMethodPage extends UIComponent {

    public cards;
    public selectCardMode = false;
    public selectedCard = null;
    public translations: any
    public title: string;

    constructor(
        public navCtrl: NavController,
        public viewCtrl: ViewController,
        public navParams: NavParams,
        public alertCtrl: AlertController,
        public loadingCtrl: LoadingController,
        public cardsService: CardsService,
        private translateService: TranslateService

    ) {
      super();
      this.selectCardMode = navParams.get("selectCardMode");
      this.translateService.get([
        'PAYMENTMETHOD',
        "Are you sure you want to delete this card?",
        'Yes, delete it',
        'Cancel',
        "OK",
        'There must be one credit card at least.'
      ]).subscribe(values => {
        this.translations = values;
        this.title = values['PAYMENTMETHOD'];
      });
    }

    selectCard(card) {
      this.selectedCard = card;
    }

    isCardSelected(card) {
      return this.selectedCard == card;
    }

    loadCards() {
      let loader = this.loadingCtrl.create();
      loader.present();
      this.cardsService.getCards().subscribe(cards => {
        loader.dismiss();
        this.cards = cards;
        if (this.cards.length == 0) {
          this.setUIBlank();
        } else {
          this.setUIIdeal();
        }
      }, error => {
        loader.dismiss();
        this.alertCtrl.create({
          message: this.cardsService.errorToString(error),
          buttons: [this.translations['OK']]
        })
      });
    }

    deleteCard(card) {
      if (this.cards.length <= 1) {
        this.alertCtrl.create({
          message: this.translations['There must be one credit card at least.'],
          buttons: [this.translations['OK']]
        }).present();
      } else {
        this.alertCtrl.create({
          message: this.translations['Are you sure you want to delete this card?'],
          buttons: [
            {
              text: this.translations['Cancel'],
              role: 'cancel'
            },
            {
              text: this.translations['Yes, delete it'],
              handler: () => {
                this.deleteCardFromServer(card);
              }
            }
          ]
        }).present();
      }
    }

    deleteCardFromServer(card) {
      let loader = this.loadingCtrl.create();
      loader.present();
      this.cardsService.deleteCard(card).subscribe(cards => {
        loader.dismiss();
        this.loadCards();
      }, error => {
        loader.dismiss();
        this.alertCtrl.create({
          message: this.cardsService.errorToString(error),
          buttons: [this.translations['OK']]
        })
      });
    }

    goToAddCardPage(){
        this.navCtrl.push(AddCardPage);
    }

    ionViewDidEnter() {
      this.selectCardMode = this.navParams.get("selectCardMode");
      this.loadCards();
    }

    ionViewDidLoad() {
      this.selectCardMode = this.navParams.get("selectCardMode");
      this.loadCards();
    }

    returnSelectedCard() {
      this.viewCtrl.dismiss({ card: this.selectedCard });
    }

    closeModal() {
      this.viewCtrl.dismiss({ card: null });
    }

  showErrorAlert(error) {
    this.alertCtrl.create({
      message: this.cardsService.errorToString(error),
      buttons: [this.translations['OK']]
    }).present();
  }



}
