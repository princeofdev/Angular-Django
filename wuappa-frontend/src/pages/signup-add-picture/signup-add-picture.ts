import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { TermsConditionsPage } from '../terms-conditions/terms-conditions';
import { UIComponent } from '../../classes/component';
import { SignupService } from '../../providers/signup-service';
import { WorkZonePage } from '../work-zone/work-zone';
import { TranslateService } from '@ngx-translate/core';

@IonicPage()
@Component({
  selector: 'page-signup-add-picture',
  templateUrl: 'signup-add-picture.html',
})
export class SignupAddPicturePage  extends UIComponent {

  image: string = null;
  private userType: any;
  public title: any;
  public registerMode: any;
  imageExist: boolean = false;
  nextDisable: boolean = false;
  constructor(public navCtrl: NavController, public navParams: NavParams, private signupService: SignupService, private translateService: TranslateService) {
    super();
    this.userType = this.signupService.getUserType();
    console.log('hola', this.userType);
    this.translateService.get(['Sign up']).subscribe(results =>{
      this.title = results['Sign up'];
    });
    this.registerMode = true;
  }

  goToTermsConditionsPage(){
    if (this.userType == 'FIN') {
      this.navCtrl.push(TermsConditionsPage);
    } else {
      this.navCtrl.push(WorkZonePage);
    }
  }

  imageUploaded(image) {
    this.image = image;
    this.imageExist = true;
    this.signupService.setProfileImage(this.image);
  }

  mandatoryPicture(){
    if(this.userType === 'PRO'){
      if (this.imageExist){
        return false;
      }else{
        return true;
      }
    }else{
      return false;
    }
  }

}
