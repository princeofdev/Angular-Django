import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { TermsConditionsMenuPage } from './terms-conditions-menu';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';

@NgModule({
  declarations: [
    TermsConditionsMenuPage,
  ],
  exports: [
    TermsConditionsMenuPage,
  ],
  imports: [
    IonicPageModule.forChild(TermsConditionsMenuPage),
    TranslateModule,
    ComponentsModule
  ],
})
export class TermsConditionsMenuPageModule {}
