angular.module("BongApp", [
    "ui.router",
    "LocalStorageModule",
    "BongApp.Common",
    "BongApp.Auth",
    "BongApp.Subscriptions"
]).config(function($stateProvider, $urlRouterProvider) {
    $stateProvider
        .state("login", {
            url: "/login",
            templateUrl: "{{ angular_template('login.html') }}",
            controller: "AuthController"
        })
        .state("subscriptions", {
            url: "/subscriptions",
            templateUrl: "{{ angular_template('subscriptions.html') }}",
            controller: "SubscriptionsController"
        })
        .state("not-found", {
            url: "/not-found",
            templateUrl: "{{ angular_template('404.html') }}"
        });
    $urlRouterProvider.otherwise("/login");

}).run(function($rootScope, $state, $templateCache, $http, localStorageService){
    $rootScope.bongAuthToken = localStorageService.get("token");
    $rootScope.BASE_URL = "https://www.bong.com"
    $rootScope.$state = $state;
    $rootScope.$on("$viewContentLoaded", function() {
        $templateCache.removeAll();
    });
})
.controller("BongMainCtrl", function($scope, $http){
});
