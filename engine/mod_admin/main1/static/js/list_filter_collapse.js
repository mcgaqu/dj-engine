(function($){ $(document).ready(function(){
    $('#changelist-filter').children('h3').each(function(){
        var $title = $(this);
        $title.click(function(){
            $title.next().slideToggle();
        });
    });
  });
})(django.jQuery);

(function($){
    ListFilterCollapsePrototype = {
        bindToggle: function(){
            var that = this;
            this.$filterTitle.click(function(){
                that.$filterContent.slideToggle();
                that.$list.toggleClass('filtered');
            });
        },
        init: function(filterEl) {
            this.$filterTitle = $(filterEl).children('h2');
            this.$filterContent = $(filterEl).children('h3, ul');
            $(this.$filterTitle).css('cursor', 'pointer');
            this.$list = $('#changelist');
            this.bindToggle();
            this.$filterTitle.click(); // añadido por mc para cargar página con filtro plegado
        }
    }
    function ListFilterCollapse(filterEl) {
        this.init(filterEl);
    }
    ListFilterCollapse.prototype = ListFilterCollapsePrototype;

    $(document).ready(function(){
        $('#changelist-filter').each(function(){
            var collapser = new ListFilterCollapse(this);
        });
    });
})(django.jQuery);