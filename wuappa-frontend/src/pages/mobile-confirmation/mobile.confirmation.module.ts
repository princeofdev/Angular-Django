import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { MobileConfirmationPage } from './mobile-confirmation';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';

@NgModule({
  declarations: [
    MobileConfirmationPage
  ],
  exports: [
    MobileConfirmationPage
  ],
  imports: [
    IonicPageModule.forChild(MobileConfirmationPage),
    TranslateModule,
    ComponentsModule
    
  ],
})
export class MobileConfirmationPageModule {}
