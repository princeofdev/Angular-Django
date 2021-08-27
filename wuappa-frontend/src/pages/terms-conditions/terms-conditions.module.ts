import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { TermsConditionsPage } from './terms-conditions';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';


@NgModule({
  declarations: [
    TermsConditionsPage
  ],
  exports: [
    TermsConditionsPage
  ],
  imports: [
    IonicPageModule.forChild(TermsConditionsPage),
    TranslateModule,
    ComponentsModule
  ],
})
export class TermsConditionsPageModule {}
