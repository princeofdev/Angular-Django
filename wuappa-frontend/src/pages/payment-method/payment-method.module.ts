import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { PaymentMethodPage } from './payment-method';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';

@NgModule({
  declarations: [
    PaymentMethodPage
  ],
  exports: [
    PaymentMethodPage
  ],
  imports: [
    IonicPageModule.forChild(PaymentMethodPage),
    TranslateModule,
    ComponentsModule
    ],
})
export class PaymentMethodPageModule {}
