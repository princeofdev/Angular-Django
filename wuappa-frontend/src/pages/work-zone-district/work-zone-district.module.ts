import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { WorkZoneDistrictPage } from './work-zone-district';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';

@NgModule({
  declarations: [
    WorkZoneDistrictPage
  ],
  exports: [
    WorkZoneDistrictPage
  ],
  imports: [
    IonicPageModule.forChild(WorkZoneDistrictPage),
    TranslateModule,
    ComponentsModule
  ],
})
export class WorkZoneDistrictPageModule {}
