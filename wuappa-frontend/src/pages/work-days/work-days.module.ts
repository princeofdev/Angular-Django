import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { WorkDaysPage } from './work-days';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';

@NgModule({
  declarations: [
    WorkDaysPage
  ],
  exports: [
    WorkDaysPage
  ],
  imports: [
    IonicPageModule.forChild(WorkDaysPage),
    TranslateModule,
    ComponentsModule
  ],
})
export class WorkDaysPageModule {}
