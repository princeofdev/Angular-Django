import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { RecoverPasswordPage } from './recover-password';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';

@NgModule({
  declarations: [
    RecoverPasswordPage
  ],
  exports: [
    RecoverPasswordPage
  ],
  imports: [
    IonicPageModule.forChild(RecoverPasswordPage),
    TranslateModule,
    ComponentsModule
  ]
})
export class RecoverPasswordPageModule {}
