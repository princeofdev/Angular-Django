import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams, LoadingController, AlertController } from 'ionic-angular';
import { UIComponent } from '../../classes/component';
import { OnInit } from '@angular/core/src/metadata/lifecycle_hooks';
import { FormBuilder, Validators } from '@angular/forms';
import { HireService } from '../../providers/hire-service';
import { HomePage } from '../home/home';
import { ServicesService } from '../../providers/services-service';
import { TranslateService } from '@ngx-translate/core';
import { log } from 'util';

/**
 * Generated class for the ConfirmAddressPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-confirm-address',
  templateUrl: 'confirm-address.html',
})
export class ConfirmAddressPage extends UIComponent implements OnInit {

  private form = null;
  public title: any = '';
  public registerMode: boolean = false;
  public categories: any = [];
  private translations: any = [];

  constructor(
    public navCtrl: NavController,
    public navParams: NavParams,
    private fb: FormBuilder,
    public servicesService: ServicesService,
    private hireService: HireService,
    private loadingCtrl: LoadingController,
    private alertCtrl: AlertController,
    private translateService: TranslateService) {
    super();
    this.translateService.get(['Confirm your address', 'Loading', 'We’re sorry','There are no WUAPPERS available for your area', 'OK']).subscribe(results =>{
      this.title = results['Confirm your address'];
      this.translations = results;
    });
    this.registerMode = true;
    this.form = this.fb.group({
      city: ['',Validators.required],
      country: ['',Validators.required],
      postal_code: ['',Validators.required],
      state: ['',Validators.required],
      address: ['',Validators.required],
      address_details: ['',Validators.required],
      number: ['']
    });



    this.form.controls['city'].setValue(this.navParams.get('city'));
    this.form.controls['country'].setValue(this.navParams.get('country'));
    this.form.controls['postal_code'].setValue(this.navParams.get('postal_code'));
    this.form.controls['state'].setValue(this.navParams.get('state'));
    this.form.controls['address'].setValue(this.navParams.get('address'));
    this.form.controls['address_details'].setValue(this.navParams.get('address_details'));

    // this.translateService.get(['Loading']).subscribe(results =>{
    //   this.translations = results;
    // });

  }

  ngOnInit(){


  }

  setErrorLabel(field){
    let styles = {
      'label-error': this.form.value[field] === ''
    };
    return styles;
  }

  formIsValid(){
    return this.form.valid;
  }

  setAddressData(){
    this.hireService.setAddressData(this.form.value);
  }

  presentAlert() {
    this.alertCtrl.create({
      title: this.translations['We’re sorry'],
      subTitle: this.translations['There are no WUAPPERS available for your area'],
      buttons: [this.translations['OK']]
    }).present();
  }

  confirmAddress(){
    let loader = this.loadingCtrl.create({content: this.translations['Loading']});
    this.servicesService.getCategoriesByZip(this.form.value['postal_code']).subscribe(data => {
      this.categories = data;
      if (this.categories.length > 0) {
        console.log(this.form.value);
        
        this.setAddressData();
        this.navCtrl.push(HomePage, this.form.value);
        loader.dismiss();
      } else {
        this.presentAlert();
      }
    })
  }


}
