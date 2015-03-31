/*global $, ReconnectingWebSocket, alert, window, pipes*/
"use strict";

/**
 * Function calls across the background TCP socket. Uses JSON RPC + a queue.
 */
var client = {

    /**
     * Establishes a websocket connection with the server
     */
    connect: function (port) {
        var self = this;
        this.socket = new ReconnectingWebSocket("ws://" + window.location.hostname + ":" + port + "/websocket");

        this.socket.onmessage = function (messageEvent) {
            var jsonRpc = JSON.parse(messageEvent.data);
            if (jsonRpc.hasOwnProperty("data")) {
                $(".actual").html(jsonRpc.result.actual.toFixed(2));
                if (!$(".setpoint").is(":focus")) {
                    $(".setpoint").html(jsonRpc.result.setpoint.toFixed(2));
                }
                $(".units").html(jsonRpc.result.units);
            } else if (jsonRpc.error) {
                alert(jsonRpc.result);
            }
        };
    },

    /**
     * Sends a request to the server and queues function response
     */
    request: function (method, params) {
        // UUID code from http://stackoverflow.com/questions/105034/
        // how-to-create-a-guid-uuid-in-javascript/2117523#2117523
        var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
            return v.toString(16);
        });

        params = params || {};
        this.socket.send(JSON.stringify({method: method, id: uuid, params: params}));
    },

    setSetpoint: function (setpoint) {
        this.request("set_setpoint", {setpoint: setpoint});
    }
};
