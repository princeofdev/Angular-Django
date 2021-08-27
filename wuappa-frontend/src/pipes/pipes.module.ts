import { NgModule } from '@angular/core';
import { EscapeHtmlPipe } from './escape-html/escape-html';
@NgModule({
	declarations: [EscapeHtmlPipe],
	imports: [],
	exports: [EscapeHtmlPipe]
})
export class PipesModule {}
