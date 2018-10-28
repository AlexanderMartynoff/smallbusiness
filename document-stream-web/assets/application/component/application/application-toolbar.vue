<template>
    <nav class="application-toolbar sticky-top navbar navbar-expand-lg rounded navbar-light bg-light p-1 mb-3 border">
        <a class="navbar-brand" href="#" @click.prevent>
          <slot></slot>
        </a>
        <div class="collapse navbar-collapse">
            <ul class="navbar-nav mr-auto"></ul>
            <form class="form-inline">
                <div class="input-group">
                  <input type="text" class="form-control" placeholder="Recipient's username" aria-label="Recipient's username" aria-describedby="basic-addon2">
                  <div class="input-group-append">
                    <button class="btn btn-outline-secondary" type="button">Search</button>
                    <button class="btn btn-outline-secondary" type="button">
                        <i class="far fa-question-circle"></i>
                    </button>
                  </div>
                </div>
            </form>
        </div>
    </nav>
</template>
<script type="text/javascript">
export default {}
</script>
