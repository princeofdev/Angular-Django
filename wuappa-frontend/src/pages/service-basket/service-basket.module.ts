import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { ServiceBasketPage } from './service-basket';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';

@NgModule({
  declarations: [
    ServiceBasketPage,
  ],
  exports: [
    ServiceBasketPage
  ],
  imports: [
    IonicPageModule.forChild(ServiceBasketPage),
    TranslateModule,
    ComponentsModule
  ],
})
export class ServiceBasketPageModule {}
