import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { WorkZonePage } from './work-zone';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';

@NgModule({
  declarations: [
    WorkZonePage
  ],
  exports: [
    WorkZonePage
  ],
  imports: [
    IonicPageModule.forChild(WorkZonePage),
    TranslateModule,
    ComponentsModule
  ],
})
export class WorkZonePageModule {}
