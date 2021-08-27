import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { ChangePasswordPage } from './change-password';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';

@NgModule({
  declarations: [ChangePasswordPage],
  exports: [ChangePasswordPage],
  imports: [
    IonicPageModule.forChild(ChangePasswordPage),
    TranslateModule,
    ComponentsModule
  ],
})
export class ChangePasswordPageModule {}
