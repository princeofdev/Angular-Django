import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { CompleteRecoverPasswordPage } from './complete-recover-password';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';

@NgModule({
  declarations: [CompleteRecoverPasswordPage],
  exports: [CompleteRecoverPasswordPage],
  imports: [
    IonicPageModule.forChild(CompleteRecoverPasswordPage),
    TranslateModule,
    ComponentsModule
  ],
})
export class CompleteRecoverPasswordPageModule {}
