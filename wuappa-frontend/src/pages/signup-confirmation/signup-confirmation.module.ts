import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { SignupConfirmationPage } from './signup-confirmation';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';

@NgModule({
  declarations: [
    SignupConfirmationPage
  ],
  exports: [
    SignupConfirmationPage
  ],
  imports: [
    IonicPageModule.forChild(SignupConfirmationPage),
    TranslateModule,
    ComponentsModule
    ],
})
export class SignupConfirmationPageModule {}
