import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { FinishOrderPage } from './finish-order';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';

@NgModule({
  declarations: [FinishOrderPage],
  exports: [FinishOrderPage],
  imports: [
    IonicPageModule.forChild(FinishOrderPage),
    TranslateModule,
    ComponentsModule
  ],
})
export class FinishOrderPageModule {}
