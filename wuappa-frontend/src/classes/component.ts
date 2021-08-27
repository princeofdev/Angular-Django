export class UIComponent {

    static UI_BLANK: string = "UI_COMPONENT_STATUS_BLANK";
    static UI_IDEAL: string = "UI_COMPONENT_STATUS_IDEAL";
    static UI_PARTIAL: string = "UI_COMPONENT_STATUS_PARTIAL";
    static UI_LOADING: string = "UI_COMPONENT_STATUS_LOADING";
    static UI_ERROR: string = "UI_COMPONENT_STATUS_ERROR";
    static UI_SUCCESS: string = "UI_COMPONENT_STATUS_SUCCESS";
    static UI_EMPTY: string = "UI_COMPONENT_STATUS_EMPTY";

    protected uiStatus: string = UIComponent.UI_IDEAL;

    public isUIBlank(): boolean {
        return this.uiStatus == UIComponent.UI_BLANK;
    }

    public isUIEmpty(): boolean {
        return this.uiStatus == UIComponent.UI_EMPTY;
    }

    public isUIIdeal(): boolean {
        return this.uiStatus == UIComponent.UI_IDEAL;
    }

    public isUIPartial(): boolean {
        return this.uiStatus == UIComponent.UI_PARTIAL;
    }

    public isUILoading(): boolean {
        return this.uiStatus == UIComponent.UI_LOADING;
    }

    public isUIError(): boolean {
        return this.uiStatus == UIComponent.UI_ERROR;
    }

    public setUIBlank(): void {
        this.uiStatus = UIComponent.UI_BLANK;
    }

    public setUIEmpty(): void {
        this.uiStatus = UIComponent.UI_EMPTY;
    }

    public setUIIdeal(): void {
        this.uiStatus = UIComponent.UI_IDEAL;
    }

    public setUIPartial(): void {
        this.uiStatus = UIComponent.UI_PARTIAL;
    }

    public setUILoading(): void {
        this.uiStatus = UIComponent.UI_LOADING;
    }

    public setUISuccess(): void {
        this.uiStatus = UIComponent.UI_SUCCESS;
    }

    public setUIError(): void {
        this.uiStatus = UIComponent.UI_ERROR;
    }


}
