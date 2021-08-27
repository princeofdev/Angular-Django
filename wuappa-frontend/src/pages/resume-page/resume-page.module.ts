import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { ResumePage } from './resume-page';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';


@NgModule({
  declarations: [
    ResumePage
  ],
  exports: [
    ResumePage
  ],
  imports: [
    IonicPageModule.forChild(ResumePage),
    TranslateModule,
    ComponentsModule

  ],
})
export class ResumePageModule {}
