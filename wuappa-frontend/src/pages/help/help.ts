import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { TranslateService } from '@ngx-translate/core';

@IonicPage()
@Component({
  selector: 'page-help',
  templateUrl: 'help.html',
})
export class HelpPage {

  public title: any;
  public registerMode: any;

  constructor(
    public navCtrl: NavController,
    private translateService: TranslateService,
    public navParams: NavParams,
  ) {
    this.translateService.get(['Help & Support']).subscribe(value =>{
      this.title = value['Help & Support'];
    })
    this.registerMode = false;
  }

}
