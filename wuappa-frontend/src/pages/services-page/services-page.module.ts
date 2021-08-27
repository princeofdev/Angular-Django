import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { ServicesPage } from './services-page';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';


@NgModule({
  declarations: [
    ServicesPage
  ],
  exports: [
    ServicesPage
  ],
  imports: [
    IonicPageModule.forChild(ServicesPage),
    TranslateModule,
    ComponentsModule
  ],
})
export class ServicesPageModule {}
