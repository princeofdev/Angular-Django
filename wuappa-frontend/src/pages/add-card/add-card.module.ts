import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { AddCardPage } from './add-card';
import { ComponentsModule } from '../../components/components.module';
import { TranslateModule } from '@ngx-translate/core';

@NgModule({
  declarations: [AddCardPage],
  exports: [AddCardPage],
  imports: [
    IonicPageModule.forChild(AddCardPage),
    TranslateModule,
    ComponentsModule
  ],
})
export class AddCardPageModule {}
