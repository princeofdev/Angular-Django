import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { DocumentationPage } from './documentation-page';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';

@NgModule({
  declarations: [DocumentationPage],
  exports: [DocumentationPage],
  imports: [
    IonicPageModule.forChild(DocumentationPage),
    TranslateModule,
    ComponentsModule
  ],
})
export class DocumentationPageModule {}
