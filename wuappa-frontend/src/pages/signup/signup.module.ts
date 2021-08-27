import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { SignupPage } from './signup';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';

@NgModule({
  declarations: [
    SignupPage
  ],
  exports: [
    SignupPage
  ],
  imports: [
    IonicPageModule.forChild(SignupPage),
    TranslateModule,
    ComponentsModule
  ],
})
export class SignupPageModule {}
