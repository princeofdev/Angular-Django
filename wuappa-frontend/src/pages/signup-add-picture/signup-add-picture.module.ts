import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { SignupAddPicturePage } from './signup-add-picture';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';

@NgModule({
  declarations: [
    SignupAddPicturePage
  ],
  exports: [
    SignupAddPicturePage
  ],
  imports: [
    IonicPageModule.forChild(SignupAddPicturePage),
    TranslateModule,
    ComponentsModule
  ],
})
export class SignupAddPicturePageModule {}
