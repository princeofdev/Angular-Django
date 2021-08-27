import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { ServiceDetailPage } from './service-detail';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';

@NgModule({
  declarations: [
    ServiceDetailPage,
  ],
  imports: [
    IonicPageModule.forChild(ServiceDetailPage),
      TranslateModule,
      ComponentsModule
  ],
})
export class ServiceDetailPageModule {}
