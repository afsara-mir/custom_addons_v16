odoo.define('real_estate.tour', function(require) {
"use strict";

const {_t} = require('web.core');
const {Markup} = require('web.utils');
var tour = require('web_tour.tour');

const { markup } = owl;

tour.register("real_estate_tour", {
    url: "/web",
    rainbowMan: true,
    rainbowManMessage: markup(_t("<b>Hello</b>, Welcome to our Real Estate Application")),
    sequence: 10,
}, [tour.stepUtils.showAppsMenuItem(), {
    trigger: ".o_app[data-menu-xmlid='custom_real_estate.root_realestate_menu']",
    content: _t("Open Real Estate app to create your nre property in a few clicks."),
    position: "right",
    edition: "community"
}]);
});