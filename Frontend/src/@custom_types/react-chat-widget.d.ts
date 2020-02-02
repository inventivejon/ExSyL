import { Widget } from 'react-chat-widget';

declare module 'react-chat-widget'{
    class Widget extends React.Component<SimpleSelectProps, any> {}
    function addResponseMessage(input: String): any;
    function toggleMsgLoader();
    function setQuickButtons(input: Array<any>): any;
    function addUserMessage(input: String): any;
    function toggleWidget(): any;
}