import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { ConfirmAddressPage } from './confirm-address';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';

@NgModule({
  declarations: [
    ConfirmAddressPage,
  ],
  exports: [ConfirmAddressPage],
  imports: [
    IonicPageModule.forChild(ConfirmAddressPage),
    TranslateModule,
    ComponentsModule
  ],
})
export class ConfirmAddressPageModule {}
