import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { TranslateService } from '@ngx-translate/core';
import { UIComponent } from '../../classes/component';

/**
 * Generated class for the TermsConditionsMenuPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-terms-conditions-menu',
  templateUrl: 'terms-conditions-menu.html',
})
export class TermsConditionsMenuPage extends UIComponent {
  public title: any;
  public registerMode: any;

  constructor(
    public navCtrl: NavController,
    private translateService: TranslateService,
    public navParams: NavParams,
  ) {
    super();
    this.translateService.get(['TERMS-CONDITIONS']).subscribe(value =>{
      this.title = value['TERMS-CONDITIONS'];
    })
    this.registerMode = false;
  }
}
