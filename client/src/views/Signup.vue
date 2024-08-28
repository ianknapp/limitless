<template>
  <div class="flex min-h-full flex-1 flex-col justify-center h-screen px-6 py-10 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <img class="mx-auto h-16 w-auto" src="@/assets/icons/glyph.png" alt="ThinkNimble" />
      <h2 class="mt-4 text-center text-4xl font-bold leading-9 tracking-tight text-primary">
        Welcome to Limitless
      </h2>
      <div class="text-center text-primary pt-2 pb-4 opacity-50">
        Enter your information below to sign up.
      </div>
    </div>

    <div class="mt-6 sm:mx-auto sm:w-full sm:max-w-sm">
      <form @submit.prevent="register(form.value)">
        <div class="flex flex-col-2 gap-4">
          <InputField
            v-model:value="form.firstName.value"
            :errors="form.firstName.errors"
            @blur="form.firstName.validate()"
            placeholder="First Name"
          />
          <InputField
            v-model:value="form.lastName.value"
            :errors="form.lastName.errors"
            @blur="form.lastName.validate()"
            placeholder="Last Name"
          />
        </div>

        <div>
          <InputField
            v-model:value="form.email.value"
            :errors="form.email.errors"
            @blur="form.email.validate()"
            type="email"
            placeholder="Email"
          />
        </div>

        <div>
          <InputField
            v-model:value="form.password.value"
            :errors="form.password.errors"
            @blur="form.password.validate()"
            type="password"
            placeholder="Password"
          />
        </div>
        <div>
          <InputField
            v-model:value="form.confirmPassword.value"
            :errors="form.confirmPassword.errors"
            @blur="form.confirmPassword.validate()"
            type="password"
            placeholder="Confirm Password"
          />
        </div>
        <div class="pt-12">
          <LoadingSpinner v-if="loading" />
          <button
            v-else
            :disabled="!form.isValid"
            type="submit"
            data-cy="submit"
            class="btn--primary bg-zinc-900"
          >
            Sign Up
          </button>
        </div>
      </form>
    </div>
    <div class="m-4 flex self-center text-sm">
      <p class="mr-2 text-primary">Already have an account?</p>
      <router-link :to="{ name: 'Login' }" class="font-bold text-purple hover:underline">
        Log In
      </router-link>
    </div>
  </div>
</template>

<script>
import InputField from '@/components/inputs/InputField.vue'
import { useUsers } from '@/composables/Users'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

export default {
  name: 'Signup',
  components: {
    InputField,
    LoadingSpinner,
  },
  setup() {
    const { register, loading, registerForm } = useUsers()

    return {
      form: registerForm,
      loading,
      register,
    }
  },
}
</script>

<style scoped lang="css"></style>
