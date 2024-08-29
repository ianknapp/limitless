<template>
  <div class="flex min-h-full flex-1 flex-col justify-center h-screen px-6 py-12 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <img class="mx-auto h-16 w-auto" src="@/assets/icons/glyph.png" alt="Limitless" />
      <h2 class="mt-4 text-center text-4xl font-bold leading-9 tracking-tight text-primary">
        Welcome to Limitless
      </h2>
      <div class="text-center text-primary pt-2 pb-4 opacity-50">
        Enter your information below to log in.
      </div>
    </div>

    <div class="mt-6 sm:mx-auto sm:w-full sm:max-w-sm">
      <form @submit.prevent="login(form.value)">
        <InputField
          v-model:value="form.email.value"
          :errors="form.email.errors"
          @blur="form.email.validate()"
          inputClass="pl-10"
          type="email"
          data-cy="email"
          placeholder="Email"
          :id="form.email.id"
        />
        <div>
          <div class="mt-2">
            <InputField
              v-model:value="form.password.value"
              :errors="form.password.errors"
              @blur="form.password.validate()"
              type="password"
              data-cy="password"
              placeholder="Password"
              autocomplete="current-password"
              :id="form.password.id"
            >
            </InputField>
            <div class="text-end hover:underline">
              <router-link
                data-cy="password-reset"
                :to="{ name: 'RequestPasswordReset' }"
                class="text-xs text-primary"
                >Forgot password?</router-link
              >
            </div>
          </div>
        </div>

        <div v-if="!loading" class="pt-12">
          <button type="submit" data-cy="submit" class="btn--primary bg-zinc-900">Log In</button>
        </div>
        <div v-else>
          <LoadingSpinner />
        </div>
      </form>
    </div>
    <div class="m-4 flex self-center text-sm font-thin">
      <p class="mr-2 text-primary">Don't have an account?</p>
      <router-link :to="{ name: 'Signup' }" class="font-bold text-purple hover:underline">
        Sign up
      </router-link>
    </div>
  </div>
</template>

<script>
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import InputField from '@/components/inputs/InputField.vue'
import { useUsers } from '@/composables/Users'

export default {
  name: 'Login',
  components: {
    InputField,
    LoadingSpinner,
  },
  setup() {
    const { loginForm, loading, login } = useUsers()
    return {
      form: loginForm,
      loading,
      login,
    }
  },
}
</script>

<style scoped lang="css"></style>
